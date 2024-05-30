#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Automaton/Automaton.h"

namespace py = pybind11;

PYBIND11_MODULE(Automaton_bindings, m)
{
    py::class_<Transition>(m, "Transition")
        .def(py::init<>())
        .def_readwrite("to", &Transition::to)
        .def_readwrite("symbol", &Transition::symbol);

    py::class_<Automaton>(m, "Automaton")
        .def(py::init<>())
        .def(py::init<std::vector<std::vector<Transition>>,
                      std::vector<state_t>, state_t>())
        .def("addTransition", &Automaton::addTransition)
        .def("addFinalState", &Automaton::addFinalState)
        .def("setInitialState", &Automaton::setInitialState)
        .def("isFinalState", &Automaton::isFinalState)
        .def("getInitialState", &Automaton::getInitialState)
        .def("getNextState", &Automaton::getNextState)
        .def("isDeterministic", &Automaton::isDeterministic)
        .def("isAccepted",
             py::overload_cast<std::string>(&Automaton::isAccepted))
        .def("isAccepted",
             py::overload_cast<std::string, state_t>(&Automaton::isAccepted))
        .def("getEpsilonClosure",
             py::overload_cast<state_t>(&Automaton::getEpsilonClosure))
        .def("getEpsilonClosure", py::overload_cast<std::vector<state_t>>(
                                      &Automaton::getEpsilonClosure))
        .def("getTransitions",
             py::overload_cast<state_t, char>(&Automaton::getTransitions))
        .def("getTransitions", py::overload_cast<std::vector<state_t>, char>(
                                   &Automaton::getTransitions))
        .def("determinize", &Automaton::determinize)
        .def("getStates", &Automaton::getStates)
        .def("getTransitions", py::overload_cast<>(&Automaton::getTransitions))
        .def("getFinalStates", &Automaton::getFinalStates)
        .def_static("convertQx2Int", &Automaton::convertQx2Int);
}
