-- 1. Функция поиска по паттерну (имя, фамилия или номер телефона)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, user_name, phone_number
    FROM phonebook
    WHERE user_name ILIKE '%' || p || '%'
       OR phone_number ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;
 
-- 4. Функция пагинации (LIMIT и OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, user_name, phone_number
    FROM phonebook
    ORDER BY user_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;