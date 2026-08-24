CREATE OR REPLACE VIEW loja_itens_ativos AS
SELECT
    si.id AS item_id,
    si.name,
    si.points_cost,
    si.duration_seconds,
    r.id AS role_id,
    r.discord_role_id
FROM store_items AS si
INNER JOIN roles AS r
    ON r.id = si.role_id
WHERE si.active = 1
  AND r.active = 1;
