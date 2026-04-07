-- 2. Процедура upsert: добавить контакт или обновить телефон, если имя уже есть
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE user_name = p_name) THEN
        UPDATE phonebook SET phone_number = p_phone WHERE user_name = p_name;
    ELSE
        INSERT INTO phonebook(user_name, phone_number) VALUES(p_name, p_phone);
    END IF;
END;
$$;
 
-- 3. Bulk insert с валидацией телефона
--    Принимает массивы имён и телефонов, вставляет корректные,
--    возвращает некорректные (телефон должен содержать только цифры, +, -, пробелы, длина >= 7)
CREATE OR REPLACE FUNCTION bulk_insert_contacts(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
RETURNS TABLE(bad_name VARCHAR, bad_phone VARCHAR) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Валидация: телефон >= 7 символов и содержит только допустимые символы
        IF length(p_phones[i]) >= 7
           AND p_phones[i] ~ '^[0-9+\-\s()]+$' THEN
            -- Корректный — upsert
            IF EXISTS (SELECT 1 FROM phonebook WHERE user_name = p_names[i]) THEN
                UPDATE phonebook SET phone_number = p_phones[i] WHERE user_name = p_names[i];
            ELSE
                INSERT INTO phonebook(user_name, phone_number) VALUES(p_names[i], p_phones[i]);
            END IF;
        ELSE
            -- Некорректный — вернуть
            bad_name := p_names[i];
            bad_phone := p_phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
 
-- 5. Процедура удаления по имени или номеру телефона
CREATE OR REPLACE PROCEDURE delete_contact_by_name_or_phone(p_val VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE user_name = p_val OR phone_number = p_val;
END;
$$;