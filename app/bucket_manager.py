from bucket import *
import os
import json
import time
import shutil

BUCKETS_FILE = "buckets.json"

class BucketManager:
    buckets = {}

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.last_update = 0

    def add_bucket(self, bucket: Bucket):
        if bucket.bucket_name not in self.buckets:
            bucket.whole_path = f"{self.root_path}/{bucket.bucket_name}"
            os.mkdir(bucket.whole_path)
            self.buckets[bucket.bucket_name] = bucket
            print(f"Created bucket {bucket.bucket_name}")
            return True
        else:
            return False

    def remove_bucket(self, bucket_name: str):
        if bucket_name in self.buckets:
            bucket = self.buckets[bucket_name]
            shutil.rmtree(bucket.whole_path)
            del self.buckets[bucket_name]
            return True
        else:
            return False

    def load_state(self):
        self.buckets.clear()
        # If the buckets.json file doesn't, return
        if not os.path.exists(BUCKETS_FILE):
            print(f"No {BUCKETS_FILE}, skipping loading procedure..")
            return
        with open(BUCKETS_FILE, "r") as file:
            data = json.load(file)
            for b in data["buckets"]:
                bucket = Bucket(b["bucket_name"])
                bucket.whole_path = b["whole_path"]
                bucket.files = b["files"]
                self.buckets[bucket.bucket_name] = bucket
                print(f"Found bucket {bucket.bucket_name} in {BUCKETS_FILE}")
            self.last_update = data["last_update"]
        # TODO: Make this a proper date time rather than POSIX timestamp
        print(f"Loaded buckets from last update {self.last_update}...")

    def save_state(self):
        # For whatever reason time.time() is a float
        self.last_update = int(time.time())
        with open(BUCKETS_FILE, "w") as file:
            json.dump(self.to_dict(), file, indent=1)

    def to_dict(self):
        data = {
            "root_path": self.root_path,
            "last_update": self.last_update,
            "buckets": []
        }
        for b in self.buckets.values():
            data["buckets"].append(vars(b))
        return data