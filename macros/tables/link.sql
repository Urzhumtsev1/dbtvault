{%- macro link(src_pk, src_fk, src_ldts, src_source, source_model) -%}

    {{- adapter.dispatch('link', 'dbtvault')(src_pk=src_pk, src_fk=src_fk,
                                             src_ldts=src_ldts, src_source=src_source,
                                             source_model=source_model) -}}

{%- endmacro -%}

{%- macro default__link(src_pk, src_fk, src_ldts, src_source, source_model) -%}

{%- set source_cols = dbtvault.expand_column_list(columns=[src_pk, src_fk, src_ldts, src_source]) -%}
{%- set fk_cols = dbtvault.expand_column_list([src_fk]) -%}

{%- if model.config.materialized == 'vault_insert_by_rank' %}
    {%- set source_cols_with_rank = source_cols + [config.get('rank_column')] -%}
{%- endif -%}

{{ dbtvault.prepend_generated_by() }}

{{ 'WITH ' -}}

{%- if not (source_model is iterable and source_model is not string) -%}
    {%- set source_model = [source_model] -%}
{%- endif -%}

{%- set ns = namespace(last_cte= "") -%}

{%- for src in source_model -%}

{%- set source_number = loop.index | string -%}

row_rank_{{ source_number }} AS (
   
SELECT * FROM (   
    {%- if model.config.materialized == 'vault_insert_by_rank' %}
    SELECT {{ source_cols_with_rank | join(', ') }},
    {%- else %}
    SELECT {{ source_cols | join(', ') }},
    {%- endif %}
           ROW_NUMBER() OVER(
               PARTITION BY {{ src_pk }}
               ORDER BY {{ src_ldts }} ASC
           ) AS row_number
    FROM {{ ref(src) }}

) as l
WHERE row_number = 1

    {%- set ns.last_cte = "row_rank_{}".format(source_number) %}
),{{ "\n" if not loop.last }}
{% endfor -%}
{% if source_model | length > 1 %}
stage_union AS (
    {%- for src in source_model %}
    SELECT * FROM row_rank_{{ loop.index | string }}
    {%- if not loop.last %}
    UNION ALL
    {%- endif %}
    {%- endfor %}
    {%- set ns.last_cte = "stage_union" %}
),
{%- endif -%}
{%- if model.config.materialized == 'vault_insert_by_period' %}
stage_mat_filter AS (
    SELECT *
    FROM {{ ns.last_cte }}
    WHERE __PERIOD_FILTER__
    {%- set ns.last_cte = "stage_mat_filter" %}
),
{%- elif model.config.materialized == 'vault_insert_by_rank' %}
stage_mat_filter AS (
    SELECT *
    FROM {{ ns.last_cte }}
    WHERE __RANK_FILTER__
    {%- set ns.last_cte = "stage_mat_filter" %}
),
{% endif %}
{%- if source_model | length > 1 %}

row_rank_union AS (

    SELECT * FROM (
        SELECT *,
            ROW_NUMBER() OVER(
                PARTITION BY {{ src_pk }}
                ORDER BY {{ src_ldts }}, {{ src_source }} ASC
            ) AS row_rank_number
        FROM {{ ns.last_cte }}
        WHERE {{ dbtvault.multikey(fk_cols, condition='IS NOT NULL') }}
    ) AS a
    WHERE row_rank_number = 1
    {%- set ns.last_cte = "row_rank_union" %}
),
{% endif %}
records_to_insert AS (
    SELECT {{ dbtvault.prefix(source_cols, 'a', alias_target='target') }}
    FROM {{ ns.last_cte }} AS a
    {%- if dbtvault.is_vault_insert_by_period() or is_incremental() %}
    LEFT JOIN {{ this }} AS d
    ON a.{{ src_pk }} = d.{{ src_pk }}
    WHERE {{ dbtvault.prefix([src_pk], 'd') }} IS NULL
    {%- endif %}
)

SELECT * FROM records_to_insert

{%- endmacro -%}

{%- endmacro -%}
