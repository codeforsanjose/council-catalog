import * as React from 'react'
import { cardsContainer, darkCard, lightCard } from './scss/common'

interface HelloProps {
  name: string;
}


class HomeComponent extends React.Component<HelloProps, {}> {
  render() {
    return (
      <div style={cardsContainer()}>

          <div style={darkCard()}>
              <div style={lightCard()}>
                Welcome to Council-Catalog where you can search through meeting minutes by a keyword
              </div>
          </div>
      </div>
    )
  }
}

export default HomeComponent
