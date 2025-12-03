import tornado
import json
from typing import Any
from pydantic import TypeAdapter

from models import (
    SubmitJobRequest,
    SubmitJobResponse,
    CheckJobRequest,
    CheckJobResponse,
    ErrorResponse,
    Job,
    Status,
)


def generate_openapi_spec() -> dict[str, Any]:
    """Generate OpenAPI 3.0 specification from Pydantic models."""

    # Generate schemas using Pydantic's JSON schema generation
    # mode='serialization' generates schemas for output (what the API returns)
    schemas: dict[str, Any] = {}

    # Collect all schemas with their definitions
    models_to_include = [
        SubmitJobRequest,
        SubmitJobResponse,
        CheckJobRequest,
        CheckJobResponse,
        ErrorResponse,
        Job,
        Status,
    ]

    for model in models_to_include:
        schema = TypeAdapter(model).json_schema(mode='serialization', ref_template='#/components/schemas/{model}')

        # Extract the main schema
        if '$defs' in schema:
            # Add nested definitions to schemas
            for def_name, def_schema in schema['$defs'].items():
                schemas[def_name] = def_schema
            del schema['$defs']

        schemas[model.__name__] = schema

    # Build the OpenAPI spec
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Raijin API",
            "version": "1.0.0",
            "description": "API for submitting and checking radar computation jobs",
        },
        "servers": [
            {
                "url": "http://localhost:8888",
                "description": "Local development server",
            }
        ],
        "paths": {
            "/submit_job": {
                "post": {
                    "summary": "Submit a radar computation job",
                    "description": "Submit a job to compute radars for the specified instruments and COB date",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/SubmitJobRequest"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Job submitted successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SubmitJobResponse"
                                    }
                                }
                            },
                        },
                        "400": {
                            "description": "Invalid request",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            },
                        },
                        "500": {
                            "description": "Internal server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/check_job": {
                "post": {
                    "summary": "Check the status of a job",
                    "description": "Get the current status and details of a submitted job",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CheckJobRequest"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Job status retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/CheckJobResponse"
                                    }
                                }
                            },
                        },
                        "400": {
                            "description": "Invalid request",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            },
                        },
                        "500": {
                            "description": "Internal server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": schemas
        },
    }

    return spec


class OpenAPISpecHandler(tornado.web.RequestHandler):
    """Handler that serves the OpenAPI specification for the Raijin API."""

    async def get(self):
        """Return the OpenAPI 3.0 specification as JSON."""
        spec = generate_openapi_spec()

        self.set_header("Content-Type", "application/json")
        self.set_status(200)
        self.write(json.dumps(spec, indent=2))
