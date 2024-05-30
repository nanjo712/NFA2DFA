#include "Automaton/Automaton.h"

#include <iostream>
#include <nlohmann/json.hpp>

static int centers[100][2] = {
    {100, 100}, {140, 100}, {180, 100}, {220, 100}, {260, 100}, {300, 100},
    {340, 100}, {380, 100}, {420, 100}, {460, 100}, {100, 140}, {140, 140},
    {180, 140}, {220, 140}, {260, 140}, {300, 140}, {340, 140}, {380, 140},
    {420, 140}, {460, 140}, {100, 180}, {140, 180}, {180, 180}, {220, 180},
    {260, 180}, {300, 180}, {340, 180}, {380, 180}, {420, 180}, {460, 180},
    {100, 220}, {140, 220}, {180, 220}, {220, 220}, {260, 220}, {300, 220},
    {340, 220}, {380, 220}, {420, 220}, {460, 220}, {100, 260}, {140, 260},
    {180, 260}, {220, 260}, {260, 260}, {300, 260}, {340, 260}, {380, 260},
    {420, 260}, {460, 260}, {100, 300}, {140, 300}, {180, 300}, {220, 300},
    {260, 300}, {300, 300}, {340, 300}, {380, 300}, {420, 300}, {460, 300},
    {100, 340}, {140, 340}, {180, 340}, {220, 340}, {260, 340}, {300, 340},
    {340, 340}, {380, 340}, {420, 340}, {460, 340}, {100, 380}, {140, 380},
    {180, 380}, {220, 380}, {260, 380}, {300, 380}, {340, 380}, {380, 380},
    {420, 380}, {460, 380}, {100, 420}, {140, 420}, {180, 420}, {220, 420},
    {260, 420}, {300, 420}, {340, 420}, {380, 420}, {420, 420}, {460, 420},
    {100, 460}, {140, 460}, {180, 460}, {220, 460}, {260, 460}, {300, 460},
    {340, 460}, {380, 460}, {420, 460}, {460, 460}};

static void check_and_add(std::vector<state_t> &states, state_t state)
{
    if (std::find(states.begin(), states.end(), state) == states.end())
    {
        states.push_back(state);
    }
}

int Automaton::convertQx2Int(std::string q) { return std::stoi(q.substr(1)); }

Automaton::Automaton(){};

Automaton::Automaton(std::vector<std::vector<Transition>> transitions,
                     std::vector<state_t> finalStates, state_t initialState)
    : finalStates(finalStates),
      initialState(initialState),
      transitions(transitions)
{
    for (state_t i = 0; i < transitions.size(); i++)
    {
        states.push_back(i);
    }

    for (state_t i = 0; i < transitions.size(); i++)
    {
        for (Transition transition : transitions[i])
        {
            check_and_add(states, transition.to);
        }
    }
};

void Automaton::addTransition(state_t from, state_t to, char symbol)
{
    if (from >= transitions.size())
    {
        transitions.resize(from + 1);
    }
    transitions[from].push_back({to, symbol});
    check_and_add(states, from);
}

void Automaton::addFinalState(state_t state) { finalStates.push_back(state); }

void Automaton::setInitialState(state_t state) { initialState = state; }

bool Automaton::isFinalState(state_t state)
{
    return std::find(finalStates.begin(), finalStates.end(), state) !=
           finalStates.end();
}

state_t Automaton::getInitialState() { return initialState; }

state_t Automaton::getNextState(state_t state, char symbol)
{
    if (transitions.size() <= state) return -1;
    for (Transition transition : transitions[state])
    {
        if (transition.symbol == symbol)
        {
            return transition.to;
        }
    }
    return -1;
}

bool Automaton::isDeterministic()
{
    for (std::vector<Transition> stateTransitions : transitions)
    {
        std::vector<char> symbols;
        for (Transition transition : stateTransitions)
        {
            if (std::find(symbols.begin(), symbols.end(), transition.symbol) !=
                symbols.end())
            {
                return false;
            }
            symbols.push_back(transition.symbol);
        }
    }
    return true;
}

bool Automaton::isAccepted(std::string input)
{
    return isAccepted(input, initialState);
}

bool Automaton::isAccepted(std::string input, state_t state)
{
    if (input.empty())
    {
        return isFinalState(state);
    }
    state_t nextState = getNextState(state, input[0]);
    if (nextState == -1)
    {
        return false;
    }
    return isAccepted(input.substr(1), nextState);
}

std::vector<state_t> Automaton::getEpsilonClosure(state_t state)
{
    std::vector<state_t> closure;
    closure.push_back(state);
    for (state_t i = 0; i < closure.size(); i++)
    {
        if (transitions.size() <= closure[i]) continue;
        for (Transition transition : transitions[closure[i]])
        {
            if (transition.symbol == '\0' &&
                std::find(closure.begin(), closure.end(), transition.to) ==
                    closure.end())
            {
                closure.push_back(transition.to);
            }
        }
    }
    std::sort(closure.begin(), closure.end());
    return closure;
}

std::vector<state_t> Automaton::getEpsilonClosure(std::vector<state_t> states)
{
    std::vector<state_t> closure;
    for (state_t state : states)
    {
        std::vector<state_t> stateClosure = getEpsilonClosure(state);
        for (state_t state : stateClosure)
        {
            if (std::find(closure.begin(), closure.end(), state) ==
                closure.end())
            {
                closure.push_back(state);
            }
        }
    }
    std::sort(closure.begin(), closure.end());
    return closure;
}

std::vector<state_t> Automaton::getTransitions(state_t state, char symbol)
{
    std::vector<state_t> nextStates;
    if (transitions.size() <= state) return nextStates;
    for (Transition transition : transitions[state])
    {
        if (transition.symbol == symbol)
        {
            nextStates.push_back(transition.to);
        }
    }
    std::sort(nextStates.begin(), nextStates.end());
    return nextStates;
}

std::vector<state_t> Automaton::getTransitions(std::vector<state_t> states,
                                               char symbol)
{
    std::vector<state_t> nextStates;
    for (state_t state : states)
    {
        std::vector<state_t> stateTransitions = getTransitions(state, symbol);
        for (state_t state : stateTransitions)
        {
            if (std::find(nextStates.begin(), nextStates.end(), state) ==
                nextStates.end())
            {
                nextStates.push_back(state);
            }
        }
    }
    std::sort(nextStates.begin(), nextStates.end());
    return nextStates;
}

nlohmann::json Automaton::to_json()
{
    nlohmann::json j;
    j["start_state"] = "q" + std::to_string(initialState);
    nlohmann::json final_states_json;
    for (state_t state : finalStates)
    {
        final_states_json.push_back("q" + std::to_string(state));
    }
    nlohmann::json transitions_json;
    for (state_t i = 0; i < transitions.size(); i++)
    {
        for (Transition transition : transitions[i])
        {
            nlohmann::json transition_json;
            transition_json["from"] = "q" + std::to_string(i);
            transition_json["to"] = "q" + std::to_string(transition.to);
            transition_json["char"] = transition.symbol == '\0'
                                          ? "ε"
                                          : std::string(1, transition.symbol);
            transitions_json.push_back(transition_json);
        }
    }
    j["transitions"] = std::move(transitions_json);
    j["final_states"] = std::move(final_states_json);

    nlohmann::json state_json;
    for (state_t state : states)
    {
        state_json["q" + std::to_string(state)] = {{"x", centers[state][0]},
                                                   {"y", centers[state][1]}};
    }
    j["states"] = std::move(state_json);
    return j;
}

void Automaton::from_json(const nlohmann::json &j)
{
    nlohmann::json transitions = j["transitions"];
    for (const nlohmann::json &transition : transitions)
    {
        std::string from_s = transition["from"];
        std::string to_s = transition["to"];
        std::string symbol_s = transition["char"];

        state_t from = convertQx2Int(from_s);
        state_t to = convertQx2Int(to_s);

        if (symbol_s == "ε")
        {
            addTransition(from, to, '\0');
        }
        else
        {
            addTransition(from, to, symbol_s[0]);
        }
    }

    setInitialState(convertQx2Int(j["start_state"]));

    nlohmann::json final_states = j["final_states"];
    for (const nlohmann::json &final_state : final_states)
    {
        addFinalState(convertQx2Int(final_state));
    }
}

void Automaton::output()
{
    std::cout << "Initial state: " << initialState << std::endl;
    std::cout << "Final states: ";
    for (state_t state : finalStates)
    {
        std::cout << state << " ";
    }
    std::cout << std::endl;
    for (state_t i = 0; i < transitions.size(); i++)
    {
        for (Transition transition : transitions[i])
        {
            std::cout << i << " -> " << transition.to << " on "
                      << transition.symbol << std::endl;
        }
    }
}

Automaton Automaton::determinize()
{
    if (isDeterministic())
    {
        return *this;
    }
    std::vector<std::vector<Transition>> newTransitions;
    std::vector<state_t> newFinalStates;
    std::vector<std::vector<state_t>> newStates;
    std::vector<state_t> initialState = getEpsilonClosure(this->initialState);
    newStates.push_back(initialState);
    for (state_t i = 0; i < newStates.size(); i++)
    {
        std::vector<char> symbols;
        for (state_t state : newStates[i])
        {
            if (transitions.size() <= state) continue;
            for (Transition transition : transitions[state])
            {
                if (transition.symbol == '\0')
                {
                    continue;
                }
                if (std::find(symbols.begin(), symbols.end(),
                              transition.symbol) == symbols.end())
                {
                    symbols.push_back(transition.symbol);
                }
            }
        }
        for (char symbol : symbols)
        {
            std::vector<state_t> nextStates =
                getTransitions(newStates[i], symbol);
            std::vector<state_t> nextClosure = getEpsilonClosure(nextStates);
            if (nextClosure.empty())
            {
                continue;
            }
            if (std::find(newStates.begin(), newStates.end(), nextClosure) ==
                newStates.end())
            {
                newStates.push_back(nextClosure);
            }
            auto new_state_index =
                std::find(newStates.begin(), newStates.end(), nextClosure) -
                newStates.begin();
            if (newTransitions.size() <= i)
            {
                newTransitions.resize(i + 1);
            }
            newTransitions[i].push_back(
                {static_cast<state_t>(new_state_index), symbol});
        }
        if (std::any_of(newStates[i].begin(), newStates[i].end(),
                        [this](state_t state) { return isFinalState(state); }))
        {
            newFinalStates.push_back(i);
        }
    }
    auto initialStateIndex =
        std::find(newStates.begin(), newStates.end(), initialState) -
        newStates.begin();
    for (auto &newState : newStates)
    {
        std::cout << "New state: "
                  << std::distance(newStates.begin(),
                                   std::find(newStates.begin(), newStates.end(),
                                             newState))
                  << " with ";
        for (auto state : newState)
        {
            std::cout << state << " ";
        }
        std::cout << std::endl;
    }
    return Automaton(newTransitions, newFinalStates, initialStateIndex);
}