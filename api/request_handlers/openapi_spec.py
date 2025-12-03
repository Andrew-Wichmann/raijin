import tornado
import json


class OpenAPISpecHandler(tornado.web.RequestHandler):
    """Handler that serves the OpenAPI specification for the Raijin API."""

    async def get(self):
        """Return the OpenAPI 3.0 specification as JSON."""
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
                "schemas": {
                    "SubmitJobRequest": {
                        "type": "object",
                        "required": ["cob_date", "requests"],
                        "properties": {
                            "cob_date": {
                                "type": "string",
                                "format": "date",
                                "description": "The close of business (cob) date to pin market data to to produce radars for",
                            },
                            "requests": {
                                "type": "array",
                                "description": "The instruments to generate radars for",
                                "items": {
                                    "type": "object",
                                    "description": "Radar request for a specific instrument",
                                },
                            },
                            "group_id": {
                                "type": "string",
                                "nullable": True,
                                "description": "An optional id to correlate batched requests together.",
                            },
                            "enable_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether or not to use cache results and whether to cache results",
                            },
                        },
                    },
                    "SubmitJobResponse": {
                        "type": "object",
                        "required": ["job_id"],
                        "properties": {
                            "job_id": {
                                "type": "integer",
                                "description": "The unique identifier for the submitted job",
                            },
                            "group_id": {
                                "type": "string",
                                "nullable": True,
                                "description": "The group ID if provided in the request",
                            },
                        },
                    },
                    "CheckJobRequest": {
                        "type": "object",
                        "required": ["job_id"],
                        "properties": {
                            "job_id": {
                                "type": "integer",
                                "description": "The unique identifier of the job to check",
                            }
                        },
                    },
                    "CheckJobResponse": {
                        "type": "object",
                        "required": ["job", "status"],
                        "properties": {
                            "job": {"$ref": "#/components/schemas/Job"},
                            "status": {"$ref": "#/components/schemas/Status"},
                        },
                    },
                    "Job": {
                        "type": "object",
                        "required": ["job_id", "status"],
                        "properties": {
                            "job_id": {
                                "type": "integer",
                                "description": "The unique identifier for the job",
                            },
                            "group_id": {
                                "type": "string",
                                "nullable": True,
                                "description": "Optional group identifier",
                            },
                            "status": {"$ref": "#/components/schemas/Status"},
                        },
                    },
                    "Status": {
                        "type": "string",
                        "enum": ["NOT_FOUND", "PENDING", "COMPLETE", "FAILED"],
                        "description": "The current status of a job",
                    },
                    "ErrorResponse": {
                        "type": "object",
                        "required": ["error"],
                        "properties": {
                            "error": {
                                "type": "string",
                                "description": "Error message describing what went wrong",
                            }
                        },
                    },
                }
            },
        }

        self.set_header("Content-Type", "application/json")
        self.set_status(200)
        self.write(json.dumps(spec, indent=2))
