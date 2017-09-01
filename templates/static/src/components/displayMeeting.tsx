import * as React from 'react'

import { Meeting } from './types/types'

const displayMeeting = (meeting: Meeting, key: number) => {
    const meetingContainer = () => {
        return {
            width: '600px',
            textAlign: 'center'
        }
    }
    const meetingHeader = () => {
        return {
            fontSize: '24px',
            display: 'block',
            textAlign: 'left'
        }
    }
    const meetingContent = () => {
        return {
            fontSize: '16px',
            display: 'block',
            textAlign: 'left'
        }
    }
    return (
        <div style={meetingContainer()} key={key}>
            <div style={meetingHeader()}>
                {meeting.timestamp}
            </div>
            <hr />
            <div style={meetingContent()}>
                {meeting.meeting_content}
            </div>
        </div>
    )
}

export default displayMeeting
