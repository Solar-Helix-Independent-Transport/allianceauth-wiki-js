_find_user_query = \
'''query search_chars( $char_email: String!){
  users{
    search(query: $char_email) {
      id
      email
    }
  }
}'''

_user_single_query = \
'''query get_user($uid: Int!{
  users{
    single(id: $uid) {
      id
      email
      createdAt
      isActive
    }
  }
}'''

_get_group_list_query = \
'''query {
  groups{
    list(filter:"", orderBy:""){
      id
      name
      isSystem
    }
  }
}'''

_create_group_mutation = \
'''mutation create_group($group_name:String!){
  groups{
    create(name: $group_name){
      group{
       id
       name
      }
      responseResult {
        message
        succeeded
        errorCode
        slug
      }
    }
  }
}'''

_update_user_mutation = \
'''mutation update_user_groups(
  $group_list:[Int]!
  $name:String!
  $uid:Int!
	){
  users{
    update(
      id: $uid
      name: $name
      groups: $group_list
    ){
      responseResult {
        message
        succeeded
        errorCode
        slug
      }
    }
  }
}'''

_create_user_mutation = \
'''mutation create_user(
  $group_list: [Int]!
  $name: String!
  $pass: String!
  $email: String!
) {
  users {
    create(
      email: $email
      name: $name
      passwordRaw: $pass
      groups: $group_list
      providerKey: "local"
      sendWelcomeEmail: false
      mustChangePassword: false
    ) {
      responseResult {
        errorCode
        succeeded
        message
        slug
      }
    }
  }
}
'''
_user_password_mutation = \
'''mutation update_user(
  $password: String!
  $uid: Int!
) {
  users {
    update(
      id: $uid
      newPassword: $password
    ) {
      responseResult {
        errorCode
        succeeded
        message
        slug
      }
    }
  }
}
'''

_deactivate_user_mutation = \
'''mutation deactivate_user(
  $uid: Int!
) {
  users {
    deactivate(
        id: $uid
    ) {
      responseResult {
        errorCode
        succeeded
        message
        slug
      }
    }
  }
}
'''

_activate_user_mutation = \
'''mutation deactivate_user(
  $uid: Int!
) {
  users {
    activate(
        id: $uid
    ) {
      responseResult {
        errorCode
        succeeded
        message
        slug
      }
    }
  }
}
'''
