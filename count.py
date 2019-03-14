class Vote:
    ignore = ['undervote', 'overvote']

    def __init__(self, *args, **kwargs):
        self.first_choice = kwargs.pop('first_choice')
        self.second_choice = kwargs.pop('second_choice')
        self.third_choice = kwargs.pop('third_choice')

    def get_ranked_vote(self, eliminated_candidates):
        if self.first_choice not in eliminated_candidates \
                and self.first_choice not in self.ignore:
            return self.first_choice
        elif self.second_choice not in eliminated_candidates \
                and self.second_choice not in self.ignore:
            return self.second_choice
        elif self.third_choice not in eliminated_candidates \
                and self.third_choice not in self.ignore:
            return self.third_choice
        else:
            return None

import csv

votes = []
under_votes = []
candidates = []
eliminated_candidates = []
ignore = ['undervote', 'overvote']

with open('2017-ward-11-cvr.csv', newline='\n') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    # Skip the CSV header line
    next(csvreader, None)

    for row in csvreader:
        v = Vote(
            first_choice=row[1],
            second_choice=row[2],
            third_choice=row[3],
        )

        # Any ballot with all `undervote` is ignored
        if row[1] in ignore and row[2] in ignore and row[3] in ignore:
            under_votes.append(v)
        else:
            votes.append(v)

        if row[1] not in candidates and row[1] not in ignore:
            candidates.append(row[1])
        if row[2] not in candidates and row[2] not in ignore:
            candidates.append(row[2])
        if row[3] not in candidates and row[3] not in ignore:
            candidates.append(row[3])

# Need to use floor division
votes_needed_to_win = (len(votes) // 2) + 1
has_winner = False

print('Total Votes: {}'.format(len(votes)))
print('Total Under Votes: {}'.format(len(under_votes)))
print('Votes needed to win: {}'.format(votes_needed_to_win))
print('Candidates:')
for c in sorted(candidates):
    print('    - {}'.format(c))

round_count = -1


def calculate_percent(candidate_votes):
    return round((candidate_votes / len(votes)) * 100, 2)

while not has_winner:
    round_count += 1
    round_results = {}
    exhausted = 0

    print('')
    print('')
    print('----------')
    print('ROUND: {}'.format(round_count))
    print('----------')

    for c in candidates:
        if c not in eliminated_candidates:
            round_results[c] = 0

    for vote in votes:
        current_choice = vote.get_ranked_vote(eliminated_candidates)
        if current_choice:
            round_results[current_choice] += 1
        else:
            exhausted += 1

    round_results_sorted = sorted(round_results, key=round_results.get, reverse=True)

    for w in round_results_sorted:
        if round_results[w] >= votes_needed_to_win:
            has_winner = True
        print('{}: {} - {}%'.format(
            w,
            round_results[w],
            calculate_percent(round_results[w]))
        )

    lowest_candidate = round_results_sorted[-1]

    print('----------')
    print('Lowest Candidate: {}'.format(lowest_candidate))
    print('Exhausted: {}'.format(exhausted))

    eliminated_candidates.append(lowest_candidate)

    if len(round_results_sorted) == 2:
        has_winner = True
        import midi

    if has_winner:
        print('')
        print('')
        print('----------')
        print('Projected Winner: {}'.format(round_results_sorted[0]))
        print('----------')
    else:
        print('----------')
        print('No candidate exceeded the threshold.')
