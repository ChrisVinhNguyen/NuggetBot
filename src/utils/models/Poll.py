class Poll:
    def __init__(self, entries, result):
        self.entries = entries
        self.result = result
    
    def printResults(self):
        for entry in self.entries:
            print(entry.message)
            print(entry.votesFor)
            print(entry.votesAgainst)
            print("\n")
        print(self.result)


class PollEntry:
    def __init__(self, message, votesFor, votesAgainst):
        self.message = message
        self.votesFor = votesFor
        self.votesAgainst = votesAgainst