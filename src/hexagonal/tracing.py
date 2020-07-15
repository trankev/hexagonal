import json
import logging

import basictracer
import basictracer.recorder
import opentracing
from opentracing.scope_managers import contextvars


TRACE_LEVEL = 15


def setup_tracer(logger_namespace: str) -> basictracer.BasicTracer:
    logging.addLevelName(TRACE_LEVEL, "TRACE")

    scope_manager = contextvars.ContextVarsScopeManager()
    span_logger = logging.getLogger(logger_namespace)
    recorder = LogSpanRecorder(span_logger)
    tracer = basictracer.BasicTracer(recorder=recorder, scope_manager=scope_manager)
    tracer.register_required_propagators()
    return tracer


class LogSpanRecorder(basictracer.recorder.SpanRecorder):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def record_span(self, span: opentracing.Span) -> None:
        context = {
            "span_id": span.context.span_id,
            "tags": [
                {
                    "field": field,
                    "value": value,
                }
                for field, value in span.tags.items()
            ],
        }
        span_logger = self.logger.getChild(f"{span.operation_name}.{span.context.span_id}")
        for log in span.logs:
            log_content = {
                "context": context,
                "content": {
                    field: str(value)
                    for field, value in log.key_values.items()
                },
            }
            span_logger.info(json.dumps(log_content))
        trace_content = {
            "type": "trace",
            "context": context,
            "info": {
                "duration": span.duration,
                "parent_id": span.parent_id,
                "operation_name": span.operation_name,
            },
        }
        span_logger.log(TRACE_LEVEL, json.dumps(trace_content))
