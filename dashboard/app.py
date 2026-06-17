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
    ['Inventory', 'Add Watch', 'Stats', 'Watch Detail']
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
            # Add these lines before the dataframe display:
            col_s, col_f = st.columns([3, 1])
            search = col_s.text_input('Search model', placeholder='Daytona...')
            status_filter = col_f.selectbox('Status', ['All', 'in_stock', 'reserved', 'sold', 'consignment']
                                            )
            # Filter the list before building the DataFrame:
            filtered = watches
            if search:
                filtered = [w for w in filtered if search.lower() in (w.model or '').lower()]
            if status_filter != 'All':
                filtered = [w for w in filtered if w.status and w.status.value == status_filter]
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
    db = SessionLocal()
    watches = db.query(Watch).all()
    db.close()
    in_stock = [w for w in watches if w.status and w.status.value == 'in_stock']
    sold     = [w for w in watches if w.status and w.status.value == 'sold']
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Watches',    len(watches))
    col2.metric('In Stock',         len(in_stock))
    col3.metric('Sold',             len(sold))
    total_invested = sum(w.purchase_price or 0 for w in in_stock)
    col4.metric('Capital in Stock', f'€{total_invested:,.0f}')

# Then add the detail page handler:
elif page == 'Watch Detail':
    st.subheader('Watch Detail')
    db = SessionLocal()
    watches = db.query(Watch).all()
    if not watches:
        st.info('No watches yet.')
    else:
        # Let the user pick a watch by its model + reference
        options = {f'{w.model} {w.reference or ""} (ID {w.id})': w.id for w in watches}
        choice  = st.selectbox('Select a watch', list(options.keys()))
        watch   = db.query(Watch).get(options[choice])
        if watch:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'**Model:** {watch.model}')
                st.markdown(f'**Reference:** {watch.reference or "-"}')
                st.markdown(f'**Serial:** {watch.serial or "-"}')
                st.markdown(f'**Condition:** {watch.condition.value if watch.condition else "-"}')
            with col2:
                st.markdown(f'**Purchase Price:** €{watch.purchase_price or 0:,.0f}')
                st.markdown(f'**Target Price:** €{watch.target_price or 0:,.0f}')
                st.markdown(f'**Location:** {watch.location or "-"}')
                st.markdown(f'**Status:** {watch.status.value if watch.status else "-"}')
            # Photo gallery
            st.divider()
            st.markdown('**Photos**')
            from backend.storage import get_photos, save_photo
            from backend.models import Photo
            photos = get_photos(watch.id)
            if photos:
                cols = st.columns(min(len(photos), 3))
                for i, p in enumerate(photos):
                    cols[i % 3].image(str(p), use_container_width=True)
            else:
                st.caption('No photos yet.')
            # Upload new photos
            uploaded = st.file_uploader('Upload photos', type=['jpg','jpeg','png'],
                                        accept_multiple_files=True)
            if uploaded:
                for f in uploaded:
                    path = save_photo(watch.id, f)
                    photo = Photo(watch_id=watch.id, file_path=path)
                    db.add(photo)
                db.commit()
                st.success(f'Uploaded {len(uploaded)} photo(s).')
                st.rerun()  # refresh so photos appear immediately
    db.close()