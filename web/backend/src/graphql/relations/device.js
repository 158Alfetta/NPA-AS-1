import { deviceTC, groupTC, configDataTC} from '../../models'

deviceTC.addRelation(
    'groupData', {
        resolver: () => groupTC.getResolver('findById'),
        prepareArgs: {
            _id: (source) => source.group_id,
        },
        projection: {group_id: true},
    }
)

deviceTC.addRelation(
    'configData', {
        resolver: () => configDataTC.getResolver('findById'),
        prepareArgs: {
            _id: (source) => source.config_id,
        },
        projection: {config_id: true},
    }
)