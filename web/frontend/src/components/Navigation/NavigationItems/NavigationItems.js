import React from 'react'

import classes from './NavigationItems.module.css'

const NavigationItem = React.lazy(() =>
  import('./NavigationItem/NavigationItem')
)

const NavigationItems = (props) => {

  return (
    <ul className={classes.NavigationItems}>
      <NavigationItem link="/" clickedFromNav={props.clicked} exact>
        Landing
      </NavigationItem>
      <NavigationItem link="/devices" clickedFromNav={props.cliked} exact>
        Devices
      </NavigationItem>
      <NavigationItem link="/branches" clickedFromNav={props.cliked} exact>
        Manage Group
      </NavigationItem>
    </ul>
  )
}

export default NavigationItems
