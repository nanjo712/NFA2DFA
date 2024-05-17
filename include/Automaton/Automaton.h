#ifndef AUTOMATON_H_
#define AUTOMATON_H_

#include <string>
#include <vector>

using state_t = int;

struct Transition
{
    state_t to;
    char symbol;
};

class Automaton
{
   private:
    std::vector<std::vector<Transition>> transitions;
    std::vector<state_t> finalStates;
    state_t initialState;

   public:
    Automaton();
    Automaton(std::vector<std::vector<Transition>> transitions,
              std::vector<state_t> finalStates, state_t initialState);
    void addTransition(state_t from, state_t to, char symbol);
    void addFinalState(state_t state);
    void setInitialState(state_t state);
    bool isFinalState(state_t state);
    state_t getInitialState();
    state_t getNextState(state_t state, char symbol);
    bool isDeterministic();
    bool isAccepted(std::string input);
    bool isAccepted(std::string input, state_t state);
    std::vector<state_t> getEpsilonClosure(state_t state);
    std::vector<state_t> getEpsilonClosure(std::vector<state_t> states);
    std::vector<state_t> getTransitions(state_t state, char symbol);
    std::vector<state_t> getTransitions(std::vector<state_t> states,
                                        char symbol);

    void output();
};

#endif  // AUTOMATON_H_