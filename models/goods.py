from models.connector import query

def get_goods(user_id):
  ''' 
    20181104
    Goods have 3 sub class, colors, pens and icons.
    This function returns all goods with flag that is specified user purchase these goods.
  '''

  base_query = '''
    SELECT  goods.id AS id,
            {columns},
            IF(t.goods_id IS NULL, 0, 1) AS is_purchased
    FROM    goods
      INNER JOIN {table} ON goods.id = {table}.goods_id
      LEFT  JOIN (
        SELECT  goods_id
        FROM    users_goods
        WHERE   user_id = {user_id}
          AND   is_valid = 1
      ) AS t ON goods.id = t.goods_id
    WHERE   goods.is_valid = 1
    ORDER BY is_purchased DESC, id ASC
  '''

  colors_columns = '''colors.name AS name,
            colors.argb_code AS argb_code'''
  colors_query = base_query.format( columns=colors_columns,
                                    table='colors',
                                    user_id=user_id)
  colors = query(colors_query)

  pens_columns = '''pens.name,
            pens.texture_filename,
            pens.texture_bucket,
            pens.preview_filename,
            pens.preview_bucket'''
  pens_query = base_query.format( columns=pens_columns,
                                  table='pens',
                                  user_id=user_id)
  pens = query(pens_query)

  icons_columns = '''icons.name,
            icons.filename,
            icons.bucket'''
  icons_query = base_query.format(columns=icons_columns,
                                  table='icons',
                                  user_id=user_id)
  icons = query(icons_query)

  return {'colors': colors, 'pens': pens, 'icons': icons}

def get_icon(icon_id):
  base_query = '''
    SELECT  icons.*
    FROM    icons
      INNER JOIN goods ON icons.goods_id = goods.id
    WHERE   goods_id = {}
      AND   goods.is_valid = 1
  '''

  icon_query = base_query.format(icon_id)

  ret = query(icon_query)

  return ret
