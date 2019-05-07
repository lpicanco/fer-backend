workflow "Deploy to Heroku" {
  resolves = "release"
  on = "push"
}

action "login" {
  uses = "actions/heroku@master"
  args = "container:login"
  secrets = ["HEROKU_API_KEY"]
}

action "push" {
  uses = "actions/heroku@master"
  needs = "login"
  args = "container:push web"
  secrets = ["HEROKU_API_KEY"]
  env = {
    HEROKU_APP = "fer-backend"
  }
}

action "release" {
  uses = "actions/heroku@master"
  needs = "push"
  args = "container:release web"
  secrets = ["HEROKU_API_KEY"]
  env = {
    HEROKU_APP = "fer-backend"
  }
}
