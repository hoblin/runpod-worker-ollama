FROM hoblin/runpod-ollama:0.5.7

ARG MODEL_NAMES
ENV MODEL_NAMES=$MODEL_NAMES
ADD preload_model.sh /preload_model.sh
RUN apt-get update && apt-get install bash
RUN chmod +x /preload_model.sh && /preload_model.sh

# Copy the model to the volume
FROM hoblin/runpod-ollama:0.5.7
COPY --from=0 /runpod-volume /runpod-volume
