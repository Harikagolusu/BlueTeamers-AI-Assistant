# OmniRoute Setup Guide

## Overview
OmniRoute AI provides an OpenAI-compatible API that the BlueTeamers AI Assistant can use for fast, local LLM generation without requiring an Ollama instance.

## Configuration
Add the following to your .env:

``env
LLM_PROVIDER=omniroute
OMNIROUTE_API_KEY=<your_api_key>
OMNIROUTE_BASE_URL=https://api.omniroute.ai/v1
OMNIROUTE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
``
