# app/pipeline/orchestrator.py
from uuid import uuid4
from app.schemas.api import JobRequest, JobResponse
from app.agents.prompt_refiner import PromptRefinerAgent
from app.agents.requirements_agent import RequirementsAgent
from app.agents.missing_info_gate import MissingInfoGate
from app.agents.cad_spec_agent import CadSpecAgent
from app.agents.spec_normalizer import SpecNormalizerAgent
from app.agents.cad_planner import CadPlannerAgent
from app.agents.visual_critic import VisualCriticAgent
from app.cad.builder import CadBuilder
from app.validators.printability_validator import PrintabilityValidator
from app.validators.geometry_validator import GeometryValidator
from app.storage.jobs import create_job_dir, write_json, list_job_files


class Pipeline:
    def __init__(self):
        self.prompt_refiner = PromptRefinerAgent()
        self.requirements_agent = RequirementsAgent()
        self.missing_gate = MissingInfoGate()
        self.spec_agent = CadSpecAgent()
        self.normalizer = SpecNormalizerAgent()
        self.planner = CadPlannerAgent()
        self.builder = CadBuilder()
        self.print_validator = PrintabilityValidator()
        self.geometry_validator = GeometryValidator()
        self.visual_critic = VisualCriticAgent()

    def run(self, request: JobRequest) -> JobResponse:
        job_id = uuid4().hex[:12]
        job_dir = create_job_dir(job_id)
        stage_trace = []
        try:
            write_json(job_dir / "request.json", request.model_dump())
            refined = self.prompt_refiner.run(request.text, request.language)
            stage_trace.append({"stage": "prompt_refiner", "status": "ok", "confidence": refined.confidence})
            write_json(job_dir / "refined_prompt.json", refined.model_dump())

            requirements = self.requirements_agent.run(request.text, refined, request.material)
            stage_trace.append({"stage": "requirements", "status": "ok", "supported": requirements.supported})
            write_json(job_dir / "requirements.json", requirements.model_dump())

            allowed, gate_reason = self.missing_gate.run(requirements)
            stage_trace.append({"stage": "missing_info_gate", "status": "ok" if allowed else "blocked", "reason": gate_reason})
            if not allowed:
                report = {"status": "blocked", "stage_trace": stage_trace, "reason": gate_reason, "requirements": requirements.model_dump()}
                write_json(job_dir / "report.json", report)
                return JobResponse(job_id=job_id, status="blocked", build_allowed=False, message=gate_reason, files=list_job_files(job_dir), report=report)

            spec = self.spec_agent.run(requirements, request.quality_mode)
            normalized_spec, normalization_issues = self.normalizer.run(spec)
            stage_trace.append({"stage": "spec_normalizer", "status": "ok", "changes": len(normalization_issues)})
            write_json(job_dir / "cad_spec.raw.json", spec.model_dump())
            write_json(job_dir / "cad_spec.json", normalized_spec.model_dump())
            write_json(job_dir / "normalization.json", {"issues": [i.model_dump() for i in normalization_issues]})

            plan = self.planner.run(normalized_spec)
            stage_trace.append({"stage": "cad_planner", "status": "ok" if plan.build_allowed else "blocked"})
            write_json(job_dir / "plan.json", plan.model_dump())
            if not plan.build_allowed:
                report = {"status": "blocked", "stage_trace": stage_trace, "reason": plan.reason, "plan": plan.model_dump()}
                write_json(job_dir / "report.json", report)
                return JobResponse(job_id=job_id, status="blocked", build_allowed=False, message=plan.reason, files=list_job_files(job_dir), report=report)

            preflight = self.print_validator.run(normalized_spec)
            write_json(job_dir / "preflight_validation.json", preflight.model_dump())
            if not preflight.passed:
                report = {"status": "blocked", "stage_trace": stage_trace, "reason": "Preflight printability validation failed.", "validation": preflight.model_dump()}
                write_json(job_dir / "report.json", report)
                return JobResponse(job_id=job_id, status="blocked", build_allowed=False, message="Preflight printability validation failed", files=list_job_files(job_dir), report=report)

            build_result = self.builder.build(normalized_spec, job_dir)
            stage_trace.append({"stage": "cad_builder", "status": "ok"})
            print_report = self.print_validator.run(normalized_spec)
            geometry_report = self.geometry_validator.run(build_result.stl_path)
            visual_issues = self.visual_critic.run(normalized_spec)
            all_issues = normalization_issues + print_report.issues + geometry_report.issues + visual_issues
            passed = not any(i.severity == "error" for i in all_issues)
            validation = {"passed": passed, "issues": [i.model_dump() for i in all_issues], "metrics": {**print_report.metrics, **geometry_report.metrics}}
            write_json(job_dir / "validation.json", validation)
            report = {
                "status": "complete" if passed else "needs_fix",
                "job_id": job_id,
                "stage_trace": stage_trace,
                "build": build_result.model_dump(),
                "validation": validation,
                "assumptions": requirements.assumptions,
                "warnings": requirements.warnings,
                "risks": plan.risks,
                "operations": plan.operations,
            }
            write_json(job_dir / "report.json", report)
            return JobResponse(job_id=job_id, status=report["status"], build_allowed=True, message="Model generated" if passed else "Model generated but validation found issues", files=list_job_files(job_dir), report=report)
        except Exception as exc:
            stage_trace.append({"stage": "exception", "status": "error", "message": str(exc)})
            report = {"status": "failed", "job_id": job_id, "stage_trace": stage_trace, "error": str(exc)}
            write_json(job_dir / "report.json", report)
            return JobResponse(job_id=job_id, status="failed", build_allowed=False, message=str(exc), files=list_job_files(job_dir), report=report)


def run_pipeline(request: JobRequest) -> JobResponse:
    return Pipeline().run(request)
