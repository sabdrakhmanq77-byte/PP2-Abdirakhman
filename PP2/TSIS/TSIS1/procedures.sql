CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR    --'home' | 'work' | 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    -- id find
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;

    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);

    RAISE NOTICE 'Phone added to "%"', p_contact_name;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Find contact
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found', p_contact_name;
        RETURN;
    END IF;

    -- Find group. Create if doesnt exist
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE 'Group "%" created', p_group_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    RAISE NOTICE 'Contact "%" moved to group "%"', p_contact_name, p_group_name;
END;
$$;



CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id       INTEGER,
    name     VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS grp
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones  p ON p.contact_id = c.id
    WHERE
        c.name  ILIKE '%' || p_query || '%'   -- name
     OR c.email ILIKE '%' || p_query || '%'   -- email
     OR p.phone ILIKE '%' || p_query || '%';  -- number
END;
$$;