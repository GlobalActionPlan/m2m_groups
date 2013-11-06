from pyramid.i18n import TranslationStringFactory


m2m_groups_tsf = TranslationStringFactory('m2m_groups')


def includeme(config):
    config.scan()
    config.include('m2m_groups.models')