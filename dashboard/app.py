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

st.title('WatchTrack')
st.caption('Grey market watch inventory — internal use only')
# Sidebar navigation
page = st.sidebar.selectbox(
    'Navigate',
    ['Inventory', 'Add Watch', 'Stats']
)

# nn INVENTORY PAGE nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
if page == 'Inventory':
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

elif page == 'Add Watch':
    st.subheader('Add a New Watch')
    with st.form('add_watch_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Watch Details**')
            model     = st.text_input('Brand & Model *', placeholder='Rolex Daytona')
            reference = st.text_input('Reference',       placeholder='116500LN')
            serial    = st.text_input('Serial Number',   placeholder='X123456Y')
            condition = st.selectbox('Condition', ['very_good','like_new','new','good','fair'])
            source    = st.text_input('Bought from',     placeholder='Dealer in Hamburg')
        with col2:
            st.markdown('**Price & Location**')
            buy_price = st.number_input('Purchase Price (EUR)', min_value=0.0, step=100.0)
            target    = st.number_input('Target Price (EUR)',   min_value=0.0, step=100.0)
            location  = st.text_input('Who has it?',           placeholder='Karl')
            partner   = st.text_input('Bought by',             placeholder='Partner 1')
            status    = st.selectbox('Status', ['in_stock','reserved','consignment'])
        notes     = st.text_area('Notes (optional)')
        submitted = st.form_submit_button('Save Watch', use_container_width=True)
    # Handle submission OUTSIDE the form block
    if submitted:
        if not model:
            st.error('Model is required.')
        else:
            db = SessionLocal()
            w = Watch(
                model=model, reference=reference, serial=serial,
                purchase_price=buy_price, target_price=target,
                location=location, purchased_by=partner,
                purchased_from=source, notes=notes,
                status=status, condition=condition,
            )
            db.add(w)
            db.commit()
            db.close()
            st.success(f'Saved: {model} {reference or ""}')
            st.balloons()  # a little celebration never hurt anyone

# nn STATS (placeholder for Session 8) nnnnnnnnnnnnnnnnnnnnn
elif page == 'Stats':
    st.subheader('Statistics')
    st.info('Coming in Session 8!')