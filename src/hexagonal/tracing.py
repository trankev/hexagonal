import json
import logging

import basictracer.recorder


TRACE_LEVEL = 15


def setup_logging() -> None:
    logging.addLevelName(TRACE_LEVEL, "TRACE")


class LogSpanRecorder(basictracer.recorder.SpanRecorder):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def record_span(self, span):
        context = {
            "span_id": span.context.span_id,
            "tags": [
                {
                    "field": field,
                    "value": value,
                }
                for field, value in span.tags.items()
            ]
        }
        span_logger = self.logger.getChild(f"{span.operation_name}.{span.context.span_id}")
        for log in span.logs:
            log_content = {
                "context": context,
                "content": log.key_values,
            }
            span_logger.info(json.dumps(log_content))
        trace_content = {
            "type": "trace",
            "context": context,
            "info": {
                "duration": span.duration,
                "parent_id": span.parent_id,
            }
        }
        span_logger.log(TRACE_LEVEL, json.dumps(trace_content))
