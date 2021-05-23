import React from 'react'

import classes from './NavigationItem.module.css'
import { NavLink } from 'react-router-dom'

const NavigationItem = (props) => (
  <li className={classes.NavigationItem}>
    <NavLink
      to={props.link}
      exact={props.exact}
      activeClassName={classes.active}
      onClick={props.clickedFromNav}
    >
      {props.children}
    </NavLink>
  </li>
)

export default NavigationItem
