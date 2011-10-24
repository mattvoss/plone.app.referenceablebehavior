from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.uuid.interfaces import IUUID
from plone.indexer.decorator import indexer
from zope.app.component.hooks import getSite


@indexer(IReferenceable, IUIDCatalog)
def UID(obj):
    return IUUID(obj, None)

def _get_catalog(obj):
    try:
        return getToolByName(obj, 'uid_catalog')
    except AttributeError:
        return getToolByName(getSite(), 'uid_catalog')
        
def get_rel_path(obj):
    try:
        urlTool = getToolByName(obj, 'portal_url')
    except AttributeError:
        urlTool = getToolByName(getSite(), 'portal_url')
    
    return urlTool.getRelativeUrl(obj)

def added_handler(obj, event):
    """Index the object inside uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = get_rel_path(obj)

    uid_catalog.catalog_object(obj, path)

def modified_handler(obj, event):
    """Reindex object in uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = get_rel_path(obj)

    uid_catalog.catalog_object(obj, path)

def removed_handler(obj, event):
    """Remove object from uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = get_rel_path(obj)

    uid_catalog.uncatalog_object(path)
