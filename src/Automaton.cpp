#include "Automaton/Automaton.h"

#include <algorithm>
#include <iostream>

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

    for (state_t state : finalStates)
    {
        check_and_add(states, state);
    }

    check_and_add(states, initialState);
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
            if (transition.symbol == '\0')
            {
                return false;
            }
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

Automaton Automaton::determinize()
{
    if (isDeterministic())
    {
        return *this;
    }
    std::vector<std::vector<Transition>> newTransitions;
    std::vector<state_t> newFinalStates;
    std::vector<std::vector<state_t>> newStates;
    std::vector<state_t> initialState = {
        this->initialState};  // getEpsilonClosure(this->initialState);
    newStates.push_back(initialState);
    auto closure = getEpsilonClosure(initialState);
    if (std::any_of(closure.begin(), closure.end(),
                    [this](state_t state) { return isFinalState(state); }))
    {
        newFinalStates.push_back(0);
    }
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
                getTransitions(getEpsilonClosure(newStates[i]), symbol);
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

std::vector<state_t> Automaton::getStates() { return states; }

std::vector<std::vector<Transition>> Automaton::getTransitions()
{
    return transitions;
}

std::vector<state_t> Automaton::getFinalStates() { return finalStates; }

void Automaton::output()
{
    std::cout << "States: ";
    for (state_t state : states)
    {
        std::cout << state << " ";
    }
    std::cout << "\nInitial state: " << initialState << std::endl;
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