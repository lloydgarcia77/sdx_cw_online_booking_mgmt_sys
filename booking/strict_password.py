 def strict_password(self, password):
        MIN_LEN = 8
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']

        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                   '*', '(', ')', '<', '!']

        WITH_DIGITS = False
        WITH_LCASE_CHARS = False
        WITH_UCASE_CHARS = False
        WITH_SYMBOLS = False
        WITH_REPEATABLE_CHARS = False

        if len(password) < MIN_LEN:
            print("Your password is too short")
        else:
            for d in DIGITS:
                if d in password:
                    WITH_DIGITS = True
                    print("WITH DIGITS")
                    break
            for lc in LOCASE_CHARACTERS:
                if lc in password:
                    WITH_LCASE_CHARS = True
                    print("WITH LCASE")
                    break
            for uc in UPCASE_CHARACTERS:
                if uc in password:
                    WITH_UCASE_CHARS = True
                    print("WITH UCASE")
                    break
            for s in SYMBOLS:
                if s in password:
                    WITH_SYMBOLS = True
                    print("WITH SYMBOLS")
                    break

            for c in range(len(password)):
                index = c + 1
                if index < len(password):
                    if password[c] == password[c+1]:
                        WITH_REPEATABLE_CHARS = True
                        print("WITH REPEATABLE CHARS")

            if WITH_DIGITS and WITH_SYMBOLS and WITH_UCASE_CHARS and WITH_LCASE_CHARS and not WITH_REPEATABLE_CHARS:
                print("Your password is STRONG!!!")
                return True
            else:
                return False
