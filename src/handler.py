import runpod
from utils import JobInput
from engine import OllamaEngine


async def handler(job: any):
    # Just dump the whole input to the console and then return an {"ok": True} response
    print('Job:', job)

    job_input = JobInput(job["input"])
    engine_class = OllamaEngine
    engine = engine_class()  # Instantiate the engine

    job = engine.generate(job_input)  # Call generate with job_input

    async for batch in job:
        yield batch

# Original code from vllm runpod_wrapper.py
#async def handler(job):
#    job_input = JobInput(job["input"])
#    engine = OpenAIvLLMEngine if job_input.openai_route else vllm_engine
#    results_generator = engine.generate(job_input)
#    async for batch in results_generator:
#        yield batch

runpod.serverless.start(
    {
        "handler": handler,
        "return_aggregate_stream": True,
    }
)
