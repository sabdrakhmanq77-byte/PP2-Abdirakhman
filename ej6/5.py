word=input('')
s=word.lower()
vowel=('a', 'e', 'o', 'i', 'u')
if any(v in s for v in vowel):
    print('Yes')
else:
    print('No')