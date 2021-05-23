import { configDataTC } from '../../models'

export const createConfig = configDataTC.getResolver('createOne')
export const updateConfig = configDataTC.getResolver('updateById')
export const removeConfig = configDataTC.getResolver('removeById')