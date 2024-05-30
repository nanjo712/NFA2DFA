#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>

#include "Automaton/Automaton.h"

void printUsage(const std::string& programName)
{
    std::cout << "Usage: " << programName << " <path_to_json_file>"
              << std::endl;
}

bool parseArguments(int argc, char* argv[], std::string& filePath)
{
    if (argc != 2)
    {
        return false;
    }
    filePath = argv[1];
    return true;
}

int main(int argc, char* argv[])
{
    std::string filePath = "../nfa.json";

    // if (!parseArguments(argc, argv, filePath))
    // {
    //     printUsage(argv[0]);
    //     return 1;
    // }

    Automaton automaton;
    std::ifstream file(filePath);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return 1;
    }
    nlohmann::json j;
    file >> j;
    automaton.from_json(j);
    automaton.output();

    Automaton newAutomaton = automaton.determinize();
    newAutomaton.output();
    std::ofstream output("output.json");
    output << newAutomaton.to_json().dump(4) << std::endl;
    return 0;
}