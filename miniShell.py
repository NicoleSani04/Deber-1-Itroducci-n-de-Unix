#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    char entrada[1024];
    char *argumentos[100];

    // El bucle infinito del shell
    while (1) {
        // 1. Mostrar el prompt
        printf("mi-shell> ");
        
        // Leer la entrada del usuario
        if (!fgets(entrada, 1024, stdin)) {
            break; // Si hay un error al leer, salir
        }

        // Quitar el salto de línea (\n) del final
        entrada[strcspn(entrada, "\n")] = 0;

        // 2. Analizar (Tokenizar)
        // Separar la entrada por espacios
        int i = 0;
        argumentos[i] = strtok(entrada, " ");
        
        while (argumentos[i] != NULL) {
            i++;
            argumentos[i] = strtok(NULL, " ");
        }

        // Si el usuario solo presionó Enter, volver al inicio
        if (argumentos[0] == NULL) {
            continue;
        }

        // Comando para salir de nuestro shell
        if (strcmp(argumentos[0], "exit") == 0) {
            break;
        }

        // 3. Ejecutar
        pid_t pid = fork(); // Crear proceso hijo

        if (pid == 0) {
            // Este es el proceso hijo: intentamos ejecutar el comando
            if (execvp(argumentos[0], argumentos) == -1) {
                perror("Error al ejecutar el comando");
            }
            exit(EXIT_FAILURE); // Si execvp falla, el hijo debe morir
        } else if (pid < 0) {
            // Error al crear el hijo
            perror("Error en fork");
        } else {
            // Este es el proceso padre (nuestro shell principal)
            // Espera a que el hijo termine
            wait(NULL);
        }
    }

    return 0;
}