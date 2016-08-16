#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################
from girder.api import access
from girder.api.describe import Description
from girder.api.rest import Resource
from girder.plugins.minerva.utility.minerva_utility import addJobOutput
from girder.plugins.minerva.rest.dataset import Dataset


class GaiaAnalysis(Resource):
    def __init__(self):
        self.resourceName = 'gaia_analysis'
        self.route('POST', ('process',), self.gaiaAnalysis)

    @access.user
    def gaiaAnalysis(self, params):
        currentUser = self.getCurrentUser()
        datasetName = params['datasetName']
        gaia_json = params['process']

        minerva_metadata = {
            'dataset_type': 'geojson',
            'source_type': 'gaia_process',
            'original_type': 'json',
            'process_json': gaia_json
        }

        datasetResource = Dataset()
        dataset = datasetResource.constructDataset(
            datasetName,
            minerva_metadata,
            'created by Gaia'
        )
        # params = {
        #     'count': count
        # }

        # TODO change token to job token
        user, token = self.getCurrentUser(returnToken=True)
        kwargs = {
            'params': params,
            'user': currentUser,
            'dataset': dataset,
            'analysis': gaia_json,
            'token': token
        }

        job = self.model('job', 'jobs').createLocalJob(
            title='Gaia process: %s' % datasetName,
            user=currentUser,
            type='gaia.process',
            public=False,
            kwargs=kwargs,
            module='girder.plugins.gaia_minerva_plugin.jobs.gaia_worker',
            async=True)
        addJobOutput(job, dataset)
        self.model('job', 'jobs').scheduleJob(job)
        return job

        GaiaAnalysis.description = (
            Description('Run a Gaia process.')
            .param('datasetName', 'Name of the dataset created by this analysis.')
            .param('process', 'The process to run in Gaia JSON format')
        )
