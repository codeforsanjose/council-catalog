import * as React from 'react'
import { connect } from 'react-redux'
import * as style from 'ts-style' //ts-style is correct one
import { bindActionCreators } from 'redux'
import { searchByKeyword } from '../redux/actions/searchMeetingMinutes'
import store from "../redux/store/store"

interface SearchByKeywordState {
    keyword: string
}
interface SearchByKeywordProps {
    fetchSearchByKeyword: any
    searchByKeywordResults: any
    keyword: string
}

const keywordInput = () => {
    return style.create({
        margin: '10px',
        textAlign: 'center'
    })
}


class SearchByKeywordComponent extends React.Component<SearchByKeywordProps, SearchByKeywordState> {
    constructor(props) {
        super(props)
        this.state = {
            keyword: ''
        }
    }
    handleSearchByKeyword(event: React.MouseEvent<HTMLButtonElement>) {
        event.preventDefault()
        this.props.fetchSearchByKeyword(this.state.keyword)
    }

    handleSearchInput(event: React.ChangeEvent<HTMLInputElement>) {
        event.preventDefault()
        const keyword = event.target.value
        if (this.state.keyword !== keyword) {
            this.setState({
                keyword: keyword
            })
        }
    }

    render() {
        return (
            <div>
                <input 
                    type='text' 
                    placeholder='Address'
                    onChange={ e => this.handleSearchInput(e) }
                />
                <button
                    onClick={ e => this.handleSearchByKeyword(e) }
                >
                Submit for info
                </button>
            </div>
        )
    }
    componentWillReceiveProps(newProps) {
        this.setState({
            ...newProps.searchByKeywordResults
        })
        console.log(this.state)
    }
}
const mapStateToProps = (state) => {
        return {
                    ...state
                }
}
const mapDispatchToProps = (dispatch) => {
    return {
        fetchSearchByKeyword: (keyword) => dispatch(searchByKeyword(keyword)),
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(SearchByKeywordComponent)
