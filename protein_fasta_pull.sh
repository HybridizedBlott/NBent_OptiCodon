#!/bin/bash

# Your UniProt IDs (newline-separated)
UNIPROT_IDS=$1

# Run the mapping job
JOB_ID=$(curl -s -X POST "https://rest.uniprot.org/idmapping/run" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "from=UniProtKB_AC-ID&to=UniProtKB&ids=$UNIPROT_IDS" | jq -r .jobId)

# Wait for completion
while true; do
  STATUS=$(curl -s "https://rest.uniprot.org/idmapping/status/$JOB_ID" | jq -r .jobStatus)
  if [[ "$STATUS" == "FINISHED" ]]; then break; fi
  echo "Waiting for UniProt job $JOB_ID..."
  sleep 3
done

# Download FASTA
curl -L "https://rest.uniprot.org/idmapping/uniprotkb/results/$JOB_ID?format=fasta" >> uniprot_sequences.fasta

