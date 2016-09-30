from flask import Flask, jsonify, request
from trueskill import Rating, TrueSkill

app = Flask(__name__)

class BadRequest(Exception):
    pass

@app.route('/ratings', methods=['POST'])
def hello_world():
    if not request.is_json:
        raise BadRequest("Request must be json")

    params = request.get_json()

    environment = params.get("environment")
    results = params.get("results")
    teams = params.get("teams")

    trueskill = TrueSkill(mu = environment["mu"], sigma = environment["sigma"])

    team_ratings = []
    for team in teams:
        current_team = {}
        for rating in team:
            current_team[rating["id"]] = trueskill.create_rating(mu = rating["mu"], sigma = rating["sigma"])

        team_ratings.append(current_team)

    new_trueskill_ratings = trueskill.rate(team_ratings, results)

    new_ratings = []
    for team in new_trueskill_ratings:
        for rating_id in team.keys():
            nr = { "id": rating_id, "mu": team[rating_id].mu, "sigma": team[rating_id].sigma }
            new_ratings.append(nr)

    resp = { 'new_ratings': new_ratings }

    return jsonify(resp)

@app.errorhandler(BadRequest)
def handle_invalid_usage(error):
    response = jsonify({ "error": error.message})
    response.status_code = 400
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
