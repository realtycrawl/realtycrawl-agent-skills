#!/usr/bin/env python3
"""Capability discovery or one bounded REST request; prints the complete envelope."""
import argparse, json, sys
from client import request, RealtyCrawlError
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("method", choices=["GET","POST"])
parser.add_argument("path")
parser.add_argument("--parameters", default="{}", help="JSON query parameters or POST body")
parser.add_argument("--max-credits", type=int)
parser.add_argument("--idempotency-key")
def main():
    args=parser.parse_args()
    try:
        parameters=json.loads(args.parameters)
        if not isinstance(parameters,dict):
            raise ValueError("parameters must be a JSON object")
        print(json.dumps(request(args.method,args.path,parameters,max_credits=args.max_credits,idempotency_key=args.idempotency_key),indent=2))
    except (RealtyCrawlError, ValueError) as error:
        print(str(error),file=sys.stderr)
        return 1
    return 0
if __name__=="__main__":
    sys.exit(main())
