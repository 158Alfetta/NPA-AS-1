import { configDataTC } from '../../models'

export const findConfigDataById = configDataTC.getResolver('findById')
export const findOneConfigData = configDataTC.getResolver('findOne')