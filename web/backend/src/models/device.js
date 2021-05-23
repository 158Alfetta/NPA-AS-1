import mongoose from 'mongoose'
import { composeWithMongoose, composeWithMongooseDiscriminators } from 'graphql-compose-mongoose'

const { Schema } = mongoose

const deviceSchema = new Schema({
    username: {type: String, required:true},
    password: {type: String, required:true},
    ip_address: {type: String, required:true},
    type: {type: String, required:true},
    retrieved: {type: String, required:true},
    group_id: {type: String},
    config_id: {type: String},
})

export const deviceModel = mongoose.model('device', deviceSchema)
export const deviceTC = composeWithMongoose(deviceModel)

export default deviceModel