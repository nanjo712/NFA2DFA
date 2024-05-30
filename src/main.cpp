#include "Automaton/Automaton.h"

int main()
{
    Automaton automaton;
    automaton.addTransition(0, 1, '\0');
    automaton.setInitialState(0);
    auto a = automaton.determinize();
    a.output();
    return 0;
}