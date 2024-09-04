import json
from datetime import datetime, timedelta

class RequestCounter:
    def __init__(self, file_path='request_counts.json'):
        self.file_path = file_path
        self.counts = self._load_counts()

    def _load_counts(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_counts(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.counts, f)

    def increment_count(self, endpoint, period):
        now = datetime.now().isoformat()
        if endpoint not in self.counts:
            self.counts[endpoint] = {'daily': {'count': 0, 'reset_time': now},
                                     'monthly': {'count': 0, 'reset_time': now}}
        
        self._reset_if_needed(endpoint, period)
        self.counts[endpoint][period]['count'] += 1
        self._save_counts()

    def get_count(self, endpoint, period):
        if endpoint not in self.counts:
            return 0
        self._reset_if_needed(endpoint, period)
        return self.counts[endpoint][period]['count']

    def _reset_if_needed(self, endpoint, period):
        now = datetime.now()
        reset_time = datetime.fromisoformat(self.counts[endpoint][period]['reset_time'])
        if period == 'daily' and now - reset_time > timedelta(days=1):
            self.counts[endpoint][period] = {'count': 0, 'reset_time': now.isoformat()}
        elif period == 'monthly' and now - reset_time > timedelta(days=30):
            self.counts[endpoint][period] = {'count': 0, 'reset_time': now.isoformat()}

request_counter = RequestCounter()