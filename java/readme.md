# Compiling a command line jar executable

In this directory we include the needed java files and gradle setup to 
compile the executable jar used for testing the techniques for mannhardt
and equivalent implementation for deleoni.

## Requirements

- Java 1.8 (8)
- Gradle 8.4

## Steps to build
It is important to run these steps in gradle so that the python wrappers
at the top level are able to run the jar file. Run the following gradle commands
to build the jar.

- run  `gradle clean`
- run  `gradle installDist`
