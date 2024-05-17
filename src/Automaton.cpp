#include "Automaton/Automaton.h"

#include <iostream>

Automaton::Automaton(){};

Automaton::Automaton(std::vector<std::vector<Transition>> transitions,
                     std::vector<state_t> finalStates, state_t initialState)
    : finalStates(finalStates),
      initialState(initialState),
      transitions(transitions){};

void Automaton::addTransition(state_t from, state_t to, char symbol)
{
    if (from >= transitions.size())
    {
        transitions.resize(from + 1);
    }
    transitions[from].push_back({to, symbol});
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
    return closure;
}

std::vector<state_t> Automaton::getTransitions(state_t state, char symbol)
{
    std::vector<state_t> nextStates;
    for (Transition transition : transitions[state])
    {
        if (transition.symbol == symbol)
        {
            nextStates.push_back(transition.to);
        }
    }
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
    return nextStates;
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