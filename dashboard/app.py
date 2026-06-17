import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from backend.database import SessionLocal, create_tables
from backend.models import Watch

# Create tables if they don't exist yet (safe to call every run)
create_tables()
st.set_page_config(
    page_title='WatchTrack',
    page_icon='n',
    layout='wide'  # use the full browser width
)

st.title('n WatchTrack')
st.caption('Grey market watch inventory — internal use only')
# Sidebar navigation
page = st.sidebar.selectbox(
    'Navigate',
    ['n Inventory', 'n Add Watch', 'n Stats']
)

# nn INVENTORY PAGE nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
if page == 'n Inventory':
    st.subheader('Current Stock')
    db = SessionLocal()
    watches = db.query(Watch).all()
    db.close()
    if watches:
        data = []
        for w in watches:
            data.append({
                'ID':        w.id,
                'Model':     w.model,
                'Reference': w.reference,
                'Serial':    w.serial,
                'Buy (EUR)': w.purchase_price,
                'Target':    w.target_price,
                'Condition': w.condition.value if w.condition else '',
                'Status':    w.status.value if w.status else '',
                'Location':  w.location,
                'Partner':   w.purchased_by,
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)
        st.caption(f'{len(watches)} watches in database')
    else:
        st.info('No watches yet. Use n Add Watch in the sidebar.')
# nn ADD WATCH (placeholder for Session 6) nnnnnnnnnnnnnnnn
elif page == 'n Add Watch':
    st.subheader('Add a Watch')
    st.info('Coming in Session 6!')
# nn STATS (placeholder for Session 8) nnnnnnnnnnnnnnnnnnnnn
elif page == 'n Stats':
    st.subheader('Statistics')
    st.info('Coming in Session 8!')