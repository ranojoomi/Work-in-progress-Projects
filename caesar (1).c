#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int digit_checker(string lists);

int main(int argc, string argv[])
{
    if (argc == 2)
    {

        if (digit_checker(argv[1]))
        {
            int k = atoi(argv[1]);
            
            if (k < 0)
            {
                printf("Invalid Input\n");
                return 1;
            }
            else
            {
                string input = get_string("plaintext: ");
                printf("ciphertext: ");

                for (int i = 0; i < strlen(input); i++)
                {
                    if (isupper(input[i]))
                    {
                        printf("%c", (((input[i] + k) - 65) % 26) + 65);
                    }
                    else if (islower(input[i]))
                    {
                        printf("%c", (((input[i] + k) - 97) % 26) + 97);
                    }
                    else
                    {
                        printf("%c", input[i]);
                    }
                }
            }
        printf("\n");
        }
    }
    else
    {
        printf("%s key", argv[0]);
    }
}

int digit_checker(string lists)
{
    for (int i = 0; i < strlen(lists); i++)
    {
        if (isdigit(lists[i]))
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}