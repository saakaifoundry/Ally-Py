'''
Created on Sept 04, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for groups.
'''

from acl.api.group import IGroupService, Group
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import Handler
import logging
from ally.support.util_context import listBFS
from gui.core.config.impl.processor.synchronize.group_right_base import SynchronizeGroupsRightsHandler

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Required
    repository = requires(Context)

class Repository(Context):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    groupName = requires(str)
    children = requires(list)

@injected
@setup(Handler, name='synchronizeGroups')
class SynchronizeGroupsHandler(SynchronizeGroupsRightsHandler):
    '''
    Implementation for a processor that synchronizes the groups in the configuration file with the database.
    '''
    
    groupService = IGroupService; wire.entity('groupService')
    
    anonymousGroups = set
    # The set with the anonymous groups names
    
    def __init__(self):
        assert isinstance(self.groupService, IGroupService)
        'Invalid group service %s' % self.groupService
        assert isinstance(self.anonymousGroups, set), 'Invalid anonymous groups %s' % self.anonymousGroups
        super().__init__(Repository=Repository)
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the groups of the groups in the configuration file with the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        groupsDb = {name:name for name in self.groupService.getAll()}
        self.syncWithDatabase(self.groupService, listBFS(solicit.repository, Repository.children, Repository.groupName), groupsDb)
        
    def createEntity(self, repository, args):
        assert isinstance(repository, Repository), 'Invalid group repository %s' % repository
        group = Group()
        group.Name = repository.groupName 
        group.IsAnonymous = repository.groupName in self.anonymousGroups
        return group
