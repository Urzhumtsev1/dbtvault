from behave import fixture


@fixture
def eff_satellite_oos(context):
    """
    Define the structures and metadata to load effectivity satellites
    """

    context.hashed_columns = {
        "STG_CUSTOMER": {
            "CUSTOMER_ORDER_PK": ["CUSTOMER_ID", "ORDER_ID"],
            "CUSTOMER_PK": "CUSTOMER_ID",
            "ORDER_PK": "ORDER_ID",
            "HASHDIFF": {"is_hashdiff": True,
                         "columns": ["START_DATE", "END_DATE"]}
        }
    }

    context.vault_structure_columns = {
        "EFF_SAT_OOS": {
            "src_pk": "CUSTOMER_ORDER_PK",
            "src_dfk": ["ORDER_PK"],
            "src_sfk": "CUSTOMER_PK",
            "src_hashdiff": "HASHDIFF",
            "src_start_date": "START_DATE",
            "src_end_date": "END_DATE",
            "src_eff": "EFFECTIVE_FROM",
            "src_ldts": "LOAD_DATE",
            "src_source": "SOURCE"
        }
    }

    context.seed_config = {
        "RAW_STAGE": {
            "+column_types": {
                "CUSTOMER_ID": "NUMBER(38, 0)",
                "ORDER_ID": "VARCHAR",
                "START_DATE": "DATE",
                "END_DATE": "DATE",
                "LOAD_DATE": "DATE",
                "SOURCE": "VARCHAR"
            }
        },
        "EFF_SAT_OOS": {
            "+column_types": {
                "CUSTOMER_ORDER_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "HASHDIFF": "BINARY(16)",
                "START_DATE": "DATE",
                "END_DATE": "DATE",
                "EFFECTIVE_FROM": "DATE",
                "LOAD_DATE": "DATE",
                "SOURCE": "VARCHAR"
            }
        }
    }


@fixture
def eff_satellite_oos_testing_auto_end_dating(context):
    """
    Define the structures and metadata to load effectivity satellites
    """

    context.hashed_columns = {
        "STG_CUSTOMER_ORDER": {
            "CUSTOMER_ORDER_PK": ["CUSTOMER_ID", "ORDER_ID"],
            "CUSTOMER_PK": "CUSTOMER_ID",
            "ORDER_PK": "ORDER_ID"
        },
        "STG_ORDER_CUSTOMER": {
            "ORDER_CUSTOMER_PK": ["CUSTOMER_ID", "ORDER_ID"],
            "CUSTOMER_PK": "CUSTOMER_ID",
            "ORDER_PK": "ORDER_ID"
        }
    }

    context.vault_structure_columns = {
        "LINK_CUSTOMER_ORDER": {
            "source_model": "STG_CUSTOMER_ORDER",
            "src_pk": "CUSTOMER_ORDER_PK",
            "src_fk": ["CUSTOMER_PK", "ORDER_PK"],
            "src_ldts": "LOAD_DATETIME",
            "src_source": "SOURCE"
        },
        "LINK_ORDER_CUSTOMER": {
            "source_model": "STG_ORDER_CUSTOMER",
            "src_pk": "ORDER_CUSTOMER_PK",
            "src_fk": ["CUSTOMER_PK", "ORDER_PK"],
            "src_ldts": "LOAD_DATETIME",
            "src_source": "SOURCE"
        },
        "EFF_SAT_CUSTOMER_ORDER": {
            "source_model": "STG_CUSTOMER_ORDER",
            "src_pk": "CUSTOMER_ORDER_PK",
            "src_dfk": ["CUSTOMER_PK"],
            "src_sfk": "ORDER_PK",
            "src_start_date": "START_DATE",
            "src_end_date": "END_DATE",
            "src_eff": "EFFECTIVE_FROM",
            "src_ldts": "LOAD_DATETIME",
            "src_source": "SOURCE"
        },
        "EFF_SAT_ORDER_CUSTOMER": {
            "source_model": "STG_ORDER_CUSTOMER",
            "src_pk": "ORDER_CUSTOMER_PK",
            "src_dfk": ["ORDER_PK"],
            "src_sfk": "CUSTOMER_PK",
            "src_start_date": "START_DATE",
            "src_end_date": "END_DATE",
            "src_eff": "EFFECTIVE_FROM",
            "src_ldts": "LOAD_DATETIME",
            "src_source": "SOURCE"
        }
    }

    context.seed_config = {
        "RAW_STAGE_CUSTOMER_ORDER": {
            "+column_types": {
                "CUSTOMER_ID": "VARCHAR",
                "ORDER_ID": "VARCHAR",
                "START_DATE": "DATETIME",
                "END_DATE": "DATETIME",
                "EFFECTIVE_FROM": "DATETIME",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        },
        "RAW_STAGE_ORDER_CUSTOMER": {
            "+column_types": {
                "CUSTOMER_ID": "VARCHAR",
                "ORDER_ID": "VARCHAR",
                "START_DATE": "DATETIME",
                "END_DATE": "DATETIME",
                "EFFECTIVE_FROM": "DATETIME",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        },
        "LINK_CUSTOMER_ORDER": {
            "+column_types": {
                "CUSTOMER_ORDER_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        },
        "LINK_ORDER_CUSTOMER": {
            "+column_types": {
                "ORDER_CUSTOMER_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        },
        "EFF_SAT_CUSTOMER_ORDER": {
            "+column_types": {
                "CUSTOMER_ORDER_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "START_DATE": "DATETIME",
                "END_DATE": "DATETIME",
                "EFFECTIVE_FROM": "DATETIME",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        },
        "EFF_SAT_ORDER_CUSTOMER": {
            "+column_types": {
                "ORDER_CUSTOMER_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "START_DATE": "DATETIME",
                "END_DATE": "DATETIME",
                "EFFECTIVE_FROM": "DATETIME",
                "LOAD_DATETIME": "DATETIME",
                "SOURCE": "VARCHAR"
            }
        }
    }


@fixture
def eff_satellite_oos_multipart(context):
    """
    Define the structures and metadata to load effectivity satellites with multipart keys
    """

    context.hashed_columns = {
        "STG_CUSTOMER": {
            "CUSTOMER_ORDER_PK": ["CUSTOMER_ID", "ORDER_ID", "NATION_ID", "PLATFORM_ID", "ORGANISATION_ID"],
            "CUSTOMER_PK": "CUSTOMER_ID",
            "NATION_PK": "NATION_ID",
            "ORDER_PK": "ORDER_ID",
            "PLATFORM_PK": "PLATFORM_ID",
            "ORGANISATION_PK": "ORGANISATION_ID"
        }
    }

    context.vault_structure_columns = {
        "EFF_SAT": {
            "src_pk": "CUSTOMER_ORDER_PK",
            "src_dfk": ["ORDER_PK", "PLATFORM_PK", "ORGANISATION_PK"],
            "src_sfk": ["CUSTOMER_PK", "NATION_PK"],
            "src_start_date": "START_DATE",
            "src_end_date": "END_DATE",
            "src_eff": "EFFECTIVE_FROM",
            "src_ldts": "LOAD_DATE",
            "src_source": "SOURCE"
        }
    }

    context.seed_config = {
        "RAW_STAGE": {
            "+column_types": {
                "CUSTOMER_ID": "NUMBER(38, 0)",
                "NATION_ID": "VARCHAR",
                "ORDER_ID": "VARCHAR",
                "PLATFORM_ID": "VARCHAR",
                "ORGANISATION_ID": "VARCHAR",
                "START_DATE": "DATE",
                "END_DATE": "DATE",
                "LOAD_DATE": "DATE",
                "SOURCE": "VARCHAR"
            }
        },
        "EFF_SAT": {
            "+column_types": {
                "CUSTOMER_ORDER_PK": "BINARY(16)",
                "ORDER_PK": "BINARY(16)",
                "PLATFORM_PK": "BINARY(16)",
                "ORGANISATION_PK": "BINARY(16)",
                "CUSTOMER_PK": "BINARY(16)",
                "NATION_PK": "BINARY(16)",
                "START_DATE": "DATE",
                "END_DATE": "DATE",
                "EFFECTIVE_FROM": "DATE",
                "LOAD_DATE": "DATE",
                "SOURCE": "VARCHAR"
            }
        }
    }
