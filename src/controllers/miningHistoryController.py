from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct


def historyIndex():
    mining_process = MiningProcess.query.all()
    
    return render_template("mining_history/history_index.html", mining_process=mining_process)

