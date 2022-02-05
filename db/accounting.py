###############################################################################
# Copyright (C) 2022, created on February 05, 2022
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################

import datetime
from .base import Base
from sqlalchemy import (Column, Date, Index, Integer, String, Numeric, ForeignKey)


class AccountingRecord(Base):
    __tablename__ = 'accounting_record'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    type = Column(String)
    description = Column(String)
    cost = Column(Numeric(10, 2))
    comment = Column(String)

    user_id = Column(ForeignKey('user.id'), nullable=False)
    ix_accounting_record_user_id = Index('ix_accounting_record_user_id', user_id)
    ix_accounting_record_date = Index('ix_accounting_record_date', date)
    ix_accounting_record_type = Index('ix_accounting_record_type', type)
